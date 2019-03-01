count = 1
function Think()
	
	--[[for key,unit in pairs(location) do
		print(key,value)
	end]]

	--location = bot:GetLocation()

	local bot = GetBot();

	bot:Action_MoveDirectly(Vector(-1350.0, -150.0, 0.0));
	--[[if DotaTime() > 0 then
		--bot:ActionQueue_Delay(20);
		bot:Action_MoveDirectly(Vector(0.0, 0.0, 0.0));
	end]]--
	
	local loc = tostring(bot:GetLocation());
	local mana = tostring(bot:GetMana());
	local maxMana = tostring(bot:GetMaxMana());
	local hp = tostring(bot:GetHealth());
	local maxHp = tostring(bot:GetMaxHealth());

	local state = loc ..
		" " .. hp ..
		" " .. maxHp ..
		" " .. mana ..
		" " .. maxMana ..
		" " .. DotaTime()

	--loc;hp;maxHp;mana;maxMana;DotaTime(); escrever com uma determinada ordem e fazer o parse com a mesma ordem
	
	--print(state)

	local oldCount = count;

	local cmd = loadfile(GetScriptDirectory()..'/tmp/'..count);
	if cmd == nil then
		return		
	end


	if string.starts(cmd(), "MoveToLocation") then
		cmd_split = split(cmd());
		x = cmd_split[2];
		y = cmd_split[3];

		bot:Action_MoveDirectly(Vector(x, y, 0.0));

	elseif cmd() == 'hello' then
		print("Hi there");
		
	else
		print("");
	end

	count = count + 1;

end


function string.starts(String,Start)
	return string.sub(String,1,string.len(Start))==Start
end


--split = function(s, pattern, maxsplit)
function split(s, pattern, maxsplit)
	local pattern = pattern or ' '
	local maxsplit = maxsplit or -1
	local s = s
	local t = {}
	local patsz = #pattern
	while maxsplit ~= 0 do
		local curpos = 1
		local found = string.find(s, pattern)
		if found ~= nil then
			table.insert(t, string.sub(s, curpos, found - 1))
			curpos = found + patsz
			s = string.sub(s, curpos)
		else
			table.insert(t, string.sub(s, curpos))
			break
		end
		maxsplit = maxsplit - 1
		if maxsplit == 0 then
			table.insert(t, string.sub(s, curpos - patsz - 1))
		end
	end
	return t
end
